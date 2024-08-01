"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9849],{8237:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>r,default:()=>d,frontMatter:()=>s,metadata:()=>i,toc:()=>c});var o=t(5893),a=t(1151);const s={},r="Run TaskWeaver with Locally Deployed Not-that-Large Language Models",i={permalink:"/TaskWeaver/blog/local_llm",editUrl:"https://github.com/microsoft/TaskWeaver/tree/main/website/blog/local_llm.md",source:"@site/blog/local_llm.md",title:"Run TaskWeaver with Locally Deployed Not-that-Large Language Models",description:"The feature introduced in this blog post can cause incompatibility issue with the previous version of TaskWeaver",date:"2024-08-01T08:38:43.000Z",formattedDate:"August 1, 2024",tags:[],readingTime:5.535,hasTruncateMarker:!1,authors:[],frontMatter:{},unlisted:!1,prevItem:{title:"How to evaluate a LLM agent?",permalink:"/TaskWeaver/blog/evaluation"},nextItem:{title:"Plugins In-Depth",permalink:"/TaskWeaver/blog/plugin"}},l={authorsImageUrls:[]},c=[{value:"Motivation",id:"motivation",level:2},{value:"Constrained Generation",id:"constrained-generation",level:2},{value:"How we implemented the constrained generation in TaskWeaver",id:"how-we-implemented-the-constrained-generation-in-taskweaver",level:2},{value:"Conclusion",id:"conclusion",level:2}];function h(e){const n={a:"a",admonition:"admonition",code:"code",h2:"h2",p:"p",pre:"pre",...(0,a.a)(),...e.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.admonition,{type:"info",children:(0,o.jsxs)(n.p,{children:["The feature introduced in this blog post can cause incompatibility issue with the previous version of TaskWeaver\nif you have customized the examples for the planner and code interpreter.\nThe issue is easy to fix by changing the examples to the new schema.\nPlease refer to the ",(0,o.jsx)(n.a,{href:"#how-we-implemented-the-constrained-generation-in-taskweaver",children:"How we implemented the constrained generation in TaskWeaver"})," section for more details."]})}),"\n",(0,o.jsx)(n.h2,{id:"motivation",children:"Motivation"}),"\n",(0,o.jsxs)(n.p,{children:["We've seen many raised issues complaining that it is difficult to run TaskWeaver\nwith locally deployed non-that-large language models (LLMs), such as 7b or 13b.\nWhen we examine the issues, we find that the main problem is that the models failed\nto generate responses following our formatting instructions in the prompt. For instance,\nwe see that the planner's response does not contain a ",(0,o.jsx)(n.code,{children:"send_to"})," field, which is required\nto determine the recipient of the message."]}),"\n",(0,o.jsx)(n.p,{children:"In the past, we have tried to address this issue by adding more examples in the prompt,\nwhich however did not work well, especially for these relatively small models. Another idea\nwas to ask the model to re-generate the response if it does not follow the format.\nWe include the format error in the prompt to help the model understand the error and\ncorrect it. However, this approach also did not work well."}),"\n",(0,o.jsx)(n.h2,{id:"constrained-generation",children:"Constrained Generation"}),"\n",(0,o.jsxs)(n.p,{children:['Recently, we discovered a new approach called "Constrained Generation" that can enforce\nthe model to generate responses following the format. Popular frameworks include ',(0,o.jsx)(n.a,{href:"https://github.com/outlines-dev/outlines",children:"Outlines"}),",\n",(0,o.jsx)(n.a,{href:"https://github.com/guidance-ai/guidance",children:"Guidance"}),", ",(0,o.jsx)(n.a,{href:"https://github.com/noamgat/lm-format-enforcer/tree/main",children:"lm-format-enforcer"}),", etc.\nAll these frameworks support generating responses following a specific format, e.g., a JSON schema.\nThis makes it possible to control the output format by providing it a schema."]}),"\n",(0,o.jsxs)(n.p,{children:["In TaskWeaver, a relatively easy way to integrate this feature is to use a local deployment that supports\nboth constrained generation and OpenAI compatible API, for instance, the ",(0,o.jsx)(n.a,{href:"https://docs.vllm.ai/en/stable/serving/openai_compatible_server.html",children:"vllm"}),".\nThere are other frameworks that support constrained generation, such as llama.cpp.\nBut currently, we found that this feature is still not mature enough, so we start with vllm for experimentation."]}),"\n",(0,o.jsxs)(n.p,{children:["To run vllm, you can follow the instructions in the ",(0,o.jsx)(n.a,{href:"https://docs.vllm.ai/en/stable/serving/openai_compatible_server.html",children:"vllm documentation"}),".\nA simple example is shown below:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-shell",children:"python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-8B-Instruct --guided-decoding-backend lm-format-enforcer\n"})}),"\n",(0,o.jsxs)(n.p,{children:["where ",(0,o.jsx)(n.code,{children:"--guided-decoding-backend lm-format-enforcer"})," is used to enable the constrained generation feature and\nspecify the backend. Currently, vllm only supports ",(0,o.jsx)(n.code,{children:"lm-format-enforcer"})," and ",(0,o.jsx)(n.code,{children:"outlines"}),"."]}),"\n",(0,o.jsx)(n.p,{children:"Here is a sample code to test the vllm server:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:'from openai import OpenAI\n\njson_schema = {\n    "type": "object",\n    "properties": {\n        "country_name": {\n            "type": "string"\n        }\n    },\n    "required": ["country_name"]\n}\n\nopenai_api_key = "EMPTY"\nopenai_api_base = "http://localhost:8000/v1"\nclient = OpenAI(\n    api_key=openai_api_key,\n    base_url=openai_api_base,\n)\ncompletion = client.chat.completions.create(\n    model="meta-llama/Meta-Llama-3-8B-Instruct",\n    messages = [\n        {"role": "system", "content": "You are a helpful assistant."},\n        {"role": "user", "content": "Which country is San Francisco in?"}\n    ],\n    extra_body={\n        "guided_json": json_schema,\n        "guided_decoding_backend": "lm-format-enforcer"\n    }                           \n)\nprint("Completion result:", completion)\n'})}),"\n",(0,o.jsxs)(n.p,{children:["If you run the above code, you will get the response following the format specified in the ",(0,o.jsx)(n.code,{children:"json_schema"}),"."]}),"\n",(0,o.jsx)(n.p,{children:"After you have successfully deployed vllm, you can set the following configurations in TaskWeaver:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-json",children:'{\n    "llm.model": "meta-llama/Meta-Llama-3-8B-Instruct",\n    "llm.api_base": "http://localhost:8000/v1",\n    "llm.api_key": "null",\n    "llm.api_type": "openai",\n    "llm.openai.require_alternative_roles": false,\n    "llm.openai.support_system_role": true\n}\n'})}),"\n",(0,o.jsxs)(n.p,{children:["The ",(0,o.jsx)(n.code,{children:"llm.openai.require_alternative_roles"})," and ",(0,o.jsx)(n.code,{children:"llm.openai.support_system_role"})," configurations are\ndiscussed in the ",(0,o.jsx)(n.a,{href:"/docs/configurations/configurations_in_detail",children:"OpenAI Configuration"})," page.\nWith these configurations, TaskWeaver will send the messages to the vllm server and get the responses."]}),"\n",(0,o.jsx)(n.h2,{id:"how-we-implemented-the-constrained-generation-in-taskweaver",children:"How we implemented the constrained generation in TaskWeaver"}),"\n",(0,o.jsx)(n.p,{children:"In order to support the constrained generation in TaskWeaver, we need to provide the schema to the model.\nTherefore, we made a few changes in the code to support this feature."}),"\n",(0,o.jsxs)(n.p,{children:["First, we add a ",(0,o.jsx)(n.code,{children:"response_json_schema"})," field to the planner and code interpreter. For planner, you can find\nit in ",(0,o.jsx)(n.code,{children:"taskweaver/planner/planner_prompt.py"}),". It looks like this:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-yaml",children:'response_json_schema: |-\n  {\n    "type": "object",\n    "properties": {\n        "response": {\n            "type": "object",\n            "properties": {\n                "init_plan": {\n                    "type": "string"\n                },\n                "plan": {\n                    "type": "string"\n                },\n                "current_plan_step": {\n                    "type": "string"\n                },\n                "send_to": {\n                    "type": "string"\n                },\n                "message": {\n                    "type": "string"\n                }\n            },\n            "required": [\n                "init_plan",\n                "plan",\n                "current_plan_step",\n                "send_to",\n                "message"\n            ]\n        }\n    },\n    "required": ["response"]\n  }\n'})}),"\n",(0,o.jsxs)(n.p,{children:["If you are familiar with the previous output schema, you may notice that we have changed the ",(0,o.jsx)(n.code,{children:"response"})," field to an object\nfrom an array of elements. This is because that it is much easier to express the schema in JSON format if\nthe properties are in an object, not elements in an array."]}),"\n",(0,o.jsxs)(n.p,{children:["Correspondingly, we add a ",(0,o.jsx)(n.code,{children:"response_json_schema"})," field to the code interpreter. You can find it in ",(0,o.jsx)(n.code,{children:"taskweaver/code_interpreter/code_interpreter/code_generator_prompt.py"}),",\nwhich looks like this:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-yaml",children:'response_json_schema: |-\n    {\n        "type": "object",\n        "properties": {\n            "response": {\n                "type": "object",\n                "properties": {\n                    "thought": {\n                        "type": "string"\n                    },\n                    "reply_type": {\n                        "type": "string",\n                        "enum": ["python", "text"]\n                    },\n                    "reply_content": {\n                        "type": "string"\n                    }   \n                },\n                "required": ["thought", "reply_type", "reply_content"]\n            }\n        },\n        "required": ["response"]\n    } \n'})}),"\n",(0,o.jsxs)(n.p,{children:["We also change the ",(0,o.jsx)(n.code,{children:"response"})," field to an object from an array of elements in the code interpreter.\nA benefit of this change is that we can now easily restrict the ",(0,o.jsx)(n.code,{children:"reply_type"})," field to only two values: ",(0,o.jsx)(n.code,{children:"python"})," and ",(0,o.jsx)(n.code,{children:"text"}),",\nwhich is not possible before."]}),"\n",(0,o.jsxs)(n.p,{children:["One consequence of this change is that we need to modify the examples for the code interpreter in order\nto support the new schema. The old examples contain attachments that have the types of\n",(0,o.jsx)(n.code,{children:"python"}),", ",(0,o.jsx)(n.code,{children:"text"}),", and ",(0,o.jsx)(n.code,{children:"sample"}),", which are deprecated. We now need to change them to the new schema.\nSpecifically, we need to change the ",(0,o.jsx)(n.code,{children:"type"})," field to ",(0,o.jsx)(n.code,{children:"reply_type"})," and the ",(0,o.jsx)(n.code,{children:"content"})," field to ",(0,o.jsx)(n.code,{children:"reply_content"}),".\nFor example, the old example:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-yaml",children:'- type: python\n  content: |-\n    file_path = "/abc/def.txt"  \n\n    with open(file_path, "r") as file:  \n        file_contents = file.read()  \n        print(file_contents)\n'})}),"\n",(0,o.jsx)(n.p,{children:"should be changed to:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-yaml",children:"- type: reply_type\n  content: python # or 'text' if the old type is 'text' or 'sample'\n- type: reply_content\n  content: |-\n    file_path = \"/abc/def.txt\"  \n\n    with open(file_path, \"r\") as file:  \n        file_contents = file.read()  \n        print(file_contents)\n"})}),"\n",(0,o.jsxs)(n.p,{children:["There could be multiple ",(0,o.jsx)(n.code,{children:"thought"})," attachments in the code interpreter examples.\nBut in the new schema, there is only one ",(0,o.jsx)(n.code,{children:"thought"})," field. So we have added code to do the conversion and no\nmanual work is needed to modify the examples.\nIf you have examples, after these changes, we can now support the constrained generation in TaskWeaver."]}),"\n",(0,o.jsxs)(n.p,{children:["Second, we submit the JSON schema to the model when we need to call the endpoint,\nwhich you can find in ",(0,o.jsx)(n.code,{children:"planner.py"})," and ",(0,o.jsx)(n.code,{children:"code_generator.py"}),", respectively."]}),"\n",(0,o.jsx)(n.h2,{id:"conclusion",children:"Conclusion"}),"\n",(0,o.jsx)(n.p,{children:'In this blog post, we have introduced a new feature called "Constrained Generation" that can enforce the model to generate responses following the format.\nWe have also shown how to run TaskWeaver with locally deployed non-that-large language models (LLMs) that support constrained generation.\nWe have also explained how we implemented the constrained generation in TaskWeaver. We hope this feature can help you run TaskWeaver with LLMs more easily.\nIf you have any questions or suggestions, please feel free to contact us.'})]})}function d(e={}){const{wrapper:n}={...(0,a.a)(),...e.components};return n?(0,o.jsx)(n,{...e,children:(0,o.jsx)(h,{...e})}):h(e)}},1151:(e,n,t)=>{t.d(n,{Z:()=>i,a:()=>r});var o=t(7294);const a={},s=o.createContext(a);function r(e){const n=o.useContext(s);return o.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function i(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(a):e.components||a:r(e.components),o.createElement(s.Provider,{value:n},e.children)}}}]);