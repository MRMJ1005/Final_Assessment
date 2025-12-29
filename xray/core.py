from xray.llm import get_model
from xray.prompts import FILTER_PROMPT
from src.db_prep.db import Table
import uuid
from pydantic import BaseModel
from typing import Any
import inspect
class XRay(BaseModel):
    filter_function: Any
    result: Any
    product: Any
    

    def get_reasoning(self):
        model =  get_model()
        function_str = inspect.getsource(self.filter_function)
        reason =  model.invoke(
            FILTER_PROMPT(function_str,self.product,self.result)
        )
        return reason.content 
        


post = Table(
            id=uuid.uuid4(),
            description_product="Insulated water bottle with cup lid for office use",
            price=25,
            rating=3.1,
            reviews=1200
            )
def get_reasoning_filters(filter_function):
    model=get_model()
    return model.invoke(FILTER_PROMPT(filter_function,post,"rejected"))


dummy="""
passed = []
    rejected = []
    
    for p in products:
        if p.rating is not None and p.rating < 3.5:
            rejected.append({
                "id": str(p.id),
                # "reason": f"Rejected: rating {p.rating} < 3.5"
            })
            continue

        if p.reviews is not None and p.reviews < 100:
            rejected.append({
                "id": str(p.id),
                # "reason": f"Rejected: reviews {p.review} < 100"
            })
            continue
        
        if p.price<0.75*price or p.price>2*price:
            rejected.append({
                "id":p.id,
                "description_product":p.description_product,
                "price":p.price,
                # "reason":"Price not in range"
            })
            continue
        passed.append(p)

    return passed, rejected"""
print(get_reasoning_filters(dummy).content)