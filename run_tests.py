import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


class DetailedTestResult(unittest.TextTestResult):
    
    def startTest(self, test):
        super().startTest(test)
        self.stream.write(f"\n{'='*70}\n")
        self.stream.write(f"Запуск: {test}\n")
        self.stream.write(f"{'='*70}\n")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"УСПІШНО: {test.shortDescription() or test}\n")
    
    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"ПОМИЛКА: {test}\n")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"ПРОВАЛЕНО: {test}\n")


class DetailedTestRunner(unittest.TextTestRunner):
    resultclass = DetailedTestResult


loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py')

runner = DetailedTestRunner(verbosity=2)
result = runner.run(suite)

print(f"Всього тестів виконано: {result.testsRun}")
print(f"Успішних: {result.testsRun - len(result.failures) - len(result.errors)}")
print(f"Провалених: {len(result.failures)}")
print(f"Помилок: {len(result.errors)}")
print(f"Відсоток успішності: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
print("="*70)

if result.wasSuccessful():
    print("\nВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО\n")
else:
    print("\nВИЯВЛЕНО ПОМИЛКИ В ТЕСТАХ\n")

sys.exit(0 if result.wasSuccessful() else 1)