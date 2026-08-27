from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
encoder = HuggingFaceEncoder(name='sentence-transformers/all-MiniLM-L6-v2')
faq = Route(
    name='faq',
    utterances=[
        'How long does it take to process a refund?',
        'Do you offer international shipping?',
        'What payment methods are accepted?'
        ]
)

sql = Route(
    name='sql',
    utterances=[
        'i want to buy shoes that have 50% discount',
        'show me all the products on sale',
        'find me discounted items',
        'list all discounted products',
        'show me all discounted items'
        ]
)

router = SemanticRouter(
    encoder=encoder,
    routes=[faq, sql],
    auto_sync="local"
)

if __name__ == '__main__':
    route = router('show me all discounted items')
    assert not isinstance(route, list)
    print(route.name)


    # python .\E-Commerce_ChatBot\App\router.py