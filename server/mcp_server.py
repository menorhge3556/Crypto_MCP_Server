import asyncio

class CryptoMCPServer:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, handler: callable, input_schema: dict, output_schema: dict, streaming: bool = False):
        self.tools[name] = {
            "handler": handler,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "streaming": streaming
        }

    async def run(self):
        print("Crypto MCP Server is running...")

        while True:

            try:
                import sys, json

                raw = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )

                if not raw:
                    continue

                request = json.loads(raw)

                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                # Handle tool calls
                if method == "call_tool":
                    tool_name = params["name"]
                    tool_args = params.get("arguments", {})

                    if tool_name not in self.tools:
                        response = {
                            "id": request_id,
                            "error": f"Tool '{tool_name}' not found"
                        }
                    else:
                        handler = self.tools[tool_name]["handler"]

                        try:
                            result = await handler(**tool_args)
                            response = {
                                "id": request_id,
                                "result": result
                            }
                        except Exception as exc:
                            response = {
                                "id": request_id,
                                "error": str(exc)
                            }

                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()

            except Exception as e:
                print("Server error:", e)
