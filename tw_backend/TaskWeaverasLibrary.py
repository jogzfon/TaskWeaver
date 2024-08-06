from taskweaver.app.app import TaskWeaverApp

def initialize_taskweaver():
    app_dir = "./project/"
    app = TaskWeaverApp(app_dir=app_dir)
    return app.get_session()

def get_response(session, user_input):
    response_round = session.send_message(user_input)

    response_dict = response_round.to_dict()

    post_list = response_dict.get('post_list', [])

    if post_list:

        last_post = post_list[-1]

        return "\n" + f"{last_post.get('message', '')}"
    else:   
        return "No messages found."


def main():
    session = initialize_taskweaver()
    print("TaskWeaver initialized. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending conversation. Goodbye!")
            break
        
        get_response(session, user_input)
        # print("TaskWeaver:", response)

if __name__ == "__main__":
    main()