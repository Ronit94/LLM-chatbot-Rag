import os
from pinecone import Pinecone, ServerlessSpec
from config import index_name, pin_cone_api_key
pc = Pinecone(api_key=pin_cone_api_key)

# Now do stuff
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=1536, 
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )

