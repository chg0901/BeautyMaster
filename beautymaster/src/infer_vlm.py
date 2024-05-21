import os

from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image
from . import prompt

os.environ["CUDA_VISIBLE_DEVICES"]="0,1"


def infer_vlm_func(weight, model_candidate_clothes_list, season, weather, determine):


    backend_config = TurbomindEngineConfig(session_len=163840,  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.2, 
                                        tp=2)  # 两个显卡

    pipe = pipeline(weight+"/Qwen-VL-Chat-Int4", backend_config=backend_config) 

    images = [load_image(model_candidate_clothes) for model_candidate_clothes in model_candidate_clothes_list]
    
    vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine)
    response = pipe(vlm_prompt, images)

    # print(response.text)
    
    return response.text