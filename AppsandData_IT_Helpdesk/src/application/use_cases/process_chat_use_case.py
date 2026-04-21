"""ProcessChatUseCase — main orchestrator; routes intents and manages session."""
from __future__ import annotations
import asyncio

from src.application.dto.chat_request_dto import ChatRequestDTO
from src.application.dto.chat_response_dto import ChatResponseDTO
from src.application.services.intent_classifier import IntentClassifier
from src.application.services.response_merger import ResponseMerger
from src.application.use_cases.answer_kb_query_use_case import AnswerKBQueryUseCase
from src.application.use_cases.escalate_issue_use_case import EscalateIssueUseCase
from src.application.use_cases.manage_ticket_use_case import ManageTicketUseCase
from src.domain.ports.escalation_repository_port import IEscalationRepository
from src.domain.ports.kb_search_port import IKBSearchService
from src.domain.ports.llm_port import ILLMService
from src.domain.ports.notification_port import INotificationService
from src.domain.ports.session_repository_port import ISessionRepository
from src.domain.ports.ticket_repository_port import ITicketRepository
from src.domain.value_objects.confidence_score import ConfidenceScore
from src.domain.value_objects.intent import Intent

_ACCESS_DENIED_RESPONSE = (
    "Access denied. You do not have permission to view this document. "
    "Please contact your IT administrator if you require elevated access."
)


class ProcessChatUseCase:
    def __init__(
        self,
        ticket_repo: ITicketRepository,
        session_repo: ISessionRepository,
        escalation_repo: IEscalationRepository,
        kb_search: IKBSearchService,
        llm: ILLMService,
        notification: INotificationService,
    ) -> None:
        self._session_repo = session_repo
        self._intent_classifier = IntentClassifier(llm)
        self._kb_use_case = AnswerKBQueryUseCase(kb_search, llm)
        self._ticket_use_case = ManageTicketUseCase(ticket_repo)
        self._escalate_use_case = EscalateIssueUseCase(llm, notification, escalation_repo)

    def execute(self, request: ChatRequestDTO) -> ChatResponseDTO:
        # 1. Load or create session
        session = self._session_repo.get_or_create(request.session_id, request.user_id)
        history_dicts = [m.to_dict() for m in session.get_history(last_n=10)]

        # 2. Classify intent
        classification = self._intent_classifier.classify(request.message, history_dicts)
        intent: Intent = classification.get("intent", Intent.UNKNOWN)

        # 3. Route to appropriate use case(s)
        result = self._route(intent, classification, request, history_dicts)

        # 4. Auto-escalate on low confidence
        if (
            result.confidence_score is not None
            and ConfidenceScore(result.confidence_score).is_low_confidence()
            and result.escalation_case is None
        ):
            escalation = self._escalate_use_case.execute(
                session_id=request.session_id,
                user_id=request.user_id,
                conversation_history=history_dicts,
            )
            result = ResponseMerger.merge([result, escalation], request.session_id)

        # 5. Persist turn to session
        session.append_message("user", request.message)
        session.append_message("assistant", result.response)
        self._session_repo.save(session)

        return result

    # ── Routing ──────────────────────────────────────────────────────────────

    def _route(
        self,
        intent: Intent,
        classification: dict,
        request: ChatRequestDTO,
        history: list[dict],
    ) -> ChatResponseDTO:
        sid = request.session_id

        if intent == Intent.KB_LOOKUP:
            return self._kb_use_case.execute(
                session_id=sid,
                query=classification.get("kb_query") or request.message,
                user_role=request.user_role,
                doc_versions=classification.get("doc_versions"),
            )

        if intent in (Intent.TICKET_CREATE, Intent.TICKET_STATUS, Intent.TICKET_UPDATE):
            return self._ticket_use_case.execute(
                session_id=sid,
                intent=intent,
                user_id=request.user_id,
                title=classification.get("title", ""),
                description=request.message,
                ticket_id=classification.get("ticket_id"),
                new_status=classification.get("new_status"),
            )

        if intent == Intent.ESCALATION:
            return self._escalate_use_case.execute(
                session_id=sid,
                user_id=request.user_id,
                conversation_history=history,
            )

        if intent == Intent.MULTI_INTENT:
            return self._handle_multi_intent(classification, request)

        # UNKNOWN fallback
        return ChatResponseDTO(
            session_id=sid,
            response=(
                "I'm not sure how to help with that. "
                "You can ask me about IT procedures, create a support ticket, "
                "or request to speak with a specialist."
            ),
            sources=[],
        )

    def _handle_multi_intent(
        self, classification: dict, request: ChatRequestDTO
    ) -> ChatResponseDTO:
        """Execute KB and Ticket sub-intents concurrently with asyncio.gather."""

        async def _gather() -> list[ChatResponseDTO]:
            loop = asyncio.get_event_loop()
            tasks = []
            sub_intents: list[str] = classification.get("sub_intents", [])

            if "kb_lookup" in sub_intents:
                tasks.append(
                    loop.run_in_executor(
                        None,
                        lambda: self._kb_use_case.execute(
                            session_id=request.session_id,
                            query=classification.get("kb_query") or request.message,
                            user_role=request.user_role,
                            doc_versions=classification.get("doc_versions"),
                        ),
                    )
                )

            ticket_intent = next(
                (Intent(s) for s in sub_intents if s.startswith("ticket_")), None
            )
            if ticket_intent:
                tasks.append(
                    loop.run_in_executor(
                        None,
                        lambda: self._ticket_use_case.execute(
                            session_id=request.session_id,
                            intent=ticket_intent,
                            user_id=request.user_id,
                            ticket_id=classification.get("ticket_id"),
                        ),
                    )
                )

            return list(await asyncio.gather(*tasks))

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already inside an event loop (e.g. test environment)
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, _gather())
                    results = future.result()
            else:
                results = loop.run_until_complete(_gather())
        except RuntimeError:
            results = asyncio.run(_gather())

        return ResponseMerger.merge(results, request.session_id)
