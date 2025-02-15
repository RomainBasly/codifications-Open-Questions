from langchain.tools import Tool

class MultiplyTool:
    @staticmethod
    def multiply(a : int, b: int) -> int:
        return a*b

multiply_tool = Tool(name="Multiplication Tool", func= lambda x: MultiplyTool.multiply(x["a"], x["b"]), description="Multiplies two integers together. Input should be a dictionary {'a': int, 'b': int}.")