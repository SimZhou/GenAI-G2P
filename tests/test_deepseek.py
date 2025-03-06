import os
import unittest

from genai_g2p.provider.deepseek import DeepseekProvider

class TestDeepseekProvider(unittest.TestCase):
    def setUp(self):
        # 如果环境变量中没有 DEEPSEEK_API_KEY，则跳过后续测试
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            self.skipTest("DEEPSEEK_API_KEY not set, skipping Deepseek connectivity tests")

    def test_models(self):
        # 测试通过调用 completion 方法检测连通性
        model_list = [
            "deepseek-chat",
            "deepseek-reasoner",
        ]
        for model in model_list:
            provider = DeepseekProvider(model=model)
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