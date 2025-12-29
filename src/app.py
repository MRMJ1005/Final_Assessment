from fastapi import FastAPI,HTTPException,Depends,Query,Header
from src.db_prep.db import get_async_session,Table
from sqlalchemy.ext.asyncio import AsyncSession 
from typing import List
from sqlalchemy import func,select,or_,and_
from xray.llm import get_model
from xray.prompts import KEYWORD_GENERATION_PROMPT
from xray.core import XRay

app=FastAPI(
    title="Assessment",
    description="api to get competitive search",
    version='0.1.0',
    docs='/docs',
    redoc_url='/redocs'
)

def filter_products(product,price):
    if product.rating is not None and product.rating < 3.5:
        return "rejected"

    if product.reviews is not None and product.reviews < 100:
        return "rejected"
    
    if product.price<0.75*price or product.price>2*price:
        return "rejected"
        

    return "passed"
    

@app.get('/related-products')
async def get_related_products(product_description:str= Query(..., description="Description of the product"),
                               price:float=Query(...,description="Price of the product"),
                               session:AsyncSession=Depends(get_async_session)):
    if not product_description:
        raise HTTPException(status_code=400,detail="Product description should be provided")
    search_conditons=[]
    llm=get_model()
    keywords=llm.invoke(KEYWORD_GENERATION_PROMPT(product_description))
    keyword_list = [k.strip() for k in keywords.content.split(',')]
    for keyword in keyword_list:
        keyword_pattern=f"%{keyword}%"
        search_conditons.append(
            func.lower(Table.description_product).like(func.lower(keyword_pattern))
        )
        
    query=select(Table).where(or_(*search_conditons))
    result=await session.execute(query)
    
    products=result.scalars().all()
    
    
    result=[]
    for i in products:
        xray=XRay(filter_function=filter_products,product=i,result=filter_products(i,price))
        result.append({
           ("id",i.id),
           ("description",i.description_product),
           ("review",i.reviews),
           ("rating",i.rating),
           ("result",filter_products(i,price)),
           ("reason",xray.get_reasoning())
        }
        )
        
    

    return {
        
        "input":{
            "keywords":keywords.content
            },
        "output":{
            "count":len(products),
            "result":result
            
        }
        
    }
    


