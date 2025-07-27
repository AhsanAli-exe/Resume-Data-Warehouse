from code_1 import call_llm
import json
import os



def extract_json(content):
    start = content.find("{")
    end = content.rfind("}") + 1
    if start != -1 and end != 0:
        return content[start:end]
    else:
        return content
    

def process_resume(filename):
    #Reading the text file
    with open(filename,"r",encoding='utf-8',errors='ignore') as f:
        resume_text = f.read()
    response = call_llm(resume_text)
    
    #Extracting json from response
    clean_content = extract_json(response["content"])
    json_data = json.loads(clean_content)
    return json_data


#Saving json data of each resume to its own file in data/processed
def process_all_resumes(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        if file.endswith(".txt"):
            filePath = os.path.join(dir_path,file)
            json_data = process_resume(filePath)
            output_filename = file.replace(".txt",".json")
            with open("data/processed/"+output_filename,"w") as f:
                json.dump(json_data,f,indent = 4)
            print(f"Processed: {file} -> {output_filename}")
            

process_all_resumes("data/raw")

            
            

