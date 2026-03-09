import argparse
from pipelines.router import Router
from memory.session_memory import SessionMemory

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, required=True, help="Research topic")
    parser.add_argument("--mode", type=str, default="literature", help="literature | datascience")

    args = parser.parse_args()

    topic = args.topic
    mode = args.mode

    memory = SessionMemory()
    router = Router(memory)

    pipeline = router.route(mode)

    report = pipeline.run(topic)

    print("\nResearch Completed")
    print("Report saved.")

if __name__ == "__main__":
    main()