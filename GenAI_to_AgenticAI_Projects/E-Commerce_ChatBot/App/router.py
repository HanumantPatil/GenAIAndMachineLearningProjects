from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
encoder = HuggingFaceEncoder(name='sentence-transformers/all-MiniLM-L6-v2')
faq = Route(
    name='faq',
    utterances=[
        'How long does it take to process a refund?',
        'Do you offer international shipping?',
        'What payment methods are accepted?',
        'Can I track my order?',
        "Do I get discount with the HDFC credit card?",
        "Can I use multiple discount codes?",
        ]
)

sql = Route(
    name='sql',
    utterances=[
        'I want to buy shoes that have 50% discount',
        'show me all the products on sale',
        'find me discounted items',
        'list all discounted products',
        'show me all discounted items',
        'show me Nike shoes rated above 4.8',
        'find products from a specific brand',
        'list shoes with a rating higher than 4',
        'which products have the best ratings?',
        'find products within my price range',
        'show products cheaper than 2000 rupees',
        'list shoes by brand, price, or rating',
        ]
)

router = SemanticRouter(
    encoder=encoder,
    routes=[faq, sql],
    aggregation="max",
    auto_sync="local"
)

if __name__ == '__main__':
    route = router('show me all discounted items')
    assert not isinstance(route, list)
    print(route.name)


    # python .\E-Commerce_ChatBot\App\router.py