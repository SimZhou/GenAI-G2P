import os
import unittest

from genai_g2p.provider.volcengine import VolcEngineProvider

class TestVolcEngineProvider(unittest.TestCase):
    def setUp(self):
        # 如果环境变量中没有 ARK_API_KEY，则跳过后续测试
        self.api_key = os.getenv("ARK_API_KEY")
        if not self.api_key:
            self.skipTest("ARK_API_KEY not set, skipping VolcEngine connectivity tests")

    def test_completion_connectivity(self):
        # 测试通过调用 completion 方法检测连通性
        provider = VolcEngineProvider()
        prompt = "1+1=?"
        try:
            print("[Prompt]: ", prompt)
            result = provider.completion(prompt)
            print("[Reasoning]: ", result[0])
            print("[Result]: ", result[1])
        except Exception as e:
            self.fail(f"completion 方法抛出异常: {e}")

        # 断言返回结果为非空字符串
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) > 0, "返回的连通性测试结果不应为空")

    def test_doubao_models(self):
        # 测试通过调用 completion 方法检测连通性
        model_list = [
            "doubao-1.5-pro-32k-250115",
            "doubao-1.5-pro-256k-250115",
            "doubao-1.5-lite-32k-250115",
            "deepseek-v3-241226",
            "deepseek-r1-250120",
        ]
        for model in model_list:
            provider = VolcEngineProvider(model=model)
            prompt = "How many 'r's are there in the word 'strawberries'?"
            try:
                print("\n===== Model: {} =====".format(model))
                print("[Prompt]: ", prompt)
                result = provider.completion(prompt)
                print("[Reasoning]: ", result[0])
                print("[Result]: ", result[1])
            except Exception as e:
                self.fail(f"completion 方法抛出异常: {e}")

            # 断言返回结果为非空字符串
            self.assertIsInstance(result, tuple)
            self.assertTrue(len(result[1]) > 0, "返回的连通性测试结果不应为空")

if __name__ == "__main__":
    unittest.main()