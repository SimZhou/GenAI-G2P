import os
import unittest

from genai_g2p.provider.dashscope import DashscopeProvider

class TestDashscopeProvider(unittest.TestCase):
    def setUp(self):
        # 如果环境变量中没有 DASHSCOPE_API_KEY，则跳过后续测试
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            self.skipTest("DASHSCOPE_API_KEY not set, skipping Dashscope connectivity tests")

    def test_models(self):
        # 测试通过调用 completion 方法检测连通性
        model_list = [
            "qwen-max-2025-01-25",
            # "qwq-32b",
        ]
        for model in model_list:
            provider = DashscopeProvider(model=model)
            prompt = "How many 'r's are there in the word 'strawberries'?"
            try:
                print("\n===== Model: {} =====".format(model))
                print("[Prompt]: ", prompt)
                result = provider.completion(prompt)
                
                # reasoning_content = ""
                # content = ""
                # is_answering = False
                # for chunk in result:
                #     # If chunk.choices is empty, print usage
                #     if not chunk.choices:
                #         print("\nUsage:")
                #         print(chunk.usage)
                #     else:
                #         delta = chunk.choices[0].delta
                #         # Print reasoning content
                #         if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                #             print(delta.reasoning_content, end='', flush=True)
                #             reasoning_content += delta.reasoning_content
                #         else:
                #             if delta.content != "" and is_answering is False:
                #                 print("\n" + "=" * 20 + "content" + "=" * 20 + "\n")
                #                 is_answering = True
                #             # Print content
                #             print(delta.content, end='', flush=True)
                #             content += delta.content
            
            
                print("[Reasoning]: ", result[0])
                print("[Result]: ", result[1])
            except Exception as e:
                self.fail(f"completion 方法抛出异常: {e}")

            # 断言返回结果为非空字符串
            self.assertIsInstance(result, tuple)
            self.assertTrue(len(result[1]) > 0, "返回的连通性测试结果不应为空")

if __name__ == "__main__":
    unittest.main()