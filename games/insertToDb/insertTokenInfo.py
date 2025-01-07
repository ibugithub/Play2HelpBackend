from games.models import TokenInfo

# List of tokens with their respective symbols and contract addresses
tokens = [
    ("AI-Eco-Helper", "AIEH", "0xf8d273bdc3e392f0343c8aF7b4eD1D94c10529Ca"),
    ("AI-Customer-Service-Helper", "ACSH", "0xEE135573B92747c4133c7d4F2A62ebDD237D9EB7"),
    ("AI-Healthcare-Helper", "AIHH", "0xDB3af502Cb9b2E498dFB62748e0918E986E017ea"),
    ("AI-Animal-Helper", "AIAH", "0x622530f375779cBD235CD4A948de02489c9790a6")
]

# Loop through each token and save it to the database
for token_name, token_symbol, contract_address in tokens:
    # Save to TokenInfo table
    TokenInfo.objects.create(
        token_name=token_name,
        token_symbol=token_symbol,
        bnb_contract_address=contract_address
    )
