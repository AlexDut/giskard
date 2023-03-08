import inspect
import pickle
import sys
from pathlib import Path
from typing import Union, Callable, Any, Optional

from giskard import test
from giskard.core.core import TestFunctionMeta, SMT
from giskard.ml_worker.core.savable import Savable
from giskard.ml_worker.core.test_result import TestResult
from giskard.ml_worker.testing.registry.registry import tests_registry, get_test_uuid

Result = Union[TestResult, bool]


class GiskardTest(Savable[Any, TestFunctionMeta]):
    """
    The base class of all Giskard's tests

    The test are then executed inside the execute method
    All arguments shall be passed in the __init__ method
    It is advised to set default value for all arguments (None or actual value) in order to allow autocomplete
    """

    def __init__(self):
        test_uuid = get_test_uuid(type(self))
        meta = tests_registry.get_test(test_uuid)
        if meta is None:
            # equivalent to adding @test decorator
            test(type(self))
            meta = tests_registry.get_test(test_uuid)
        super(GiskardTest, self).__init__(type(self), meta)

    def execute(self) -> Result:
        """
        Execute the test
        :return: A SingleTestResult containing detailed information of the test execution results
        """
        pass

    @classmethod
    def _get_name(cls) -> str:
        return 'tests'

    @classmethod
    def _get_meta_class(cls) -> type(SMT):
        return TestFunctionMeta

    def _get_uuid(self) -> str:
        return get_test_uuid(type(self))

    def _should_save_locally(self) -> bool:
        return self.data.__module__.startswith('__main__')

    def _should_upload(self) -> bool:
        return self.meta.version is None

    @classmethod
    def _read_from_local_dir(cls, local_dir: Path, meta: TestFunctionMeta):
        if not meta.module.startswith('__main__'):
            func = getattr(sys.modules[meta.module], meta.name)
        else:
            if not local_dir.exists():
                return None
            with open(Path(local_dir) / 'data.pkl', 'rb') as f:
                func = pickle.load(f)

        if inspect.isclass(func):
            giskard_test = func()
        else:
            giskard_test = GiskardTestMethod(func)

        tests_registry.add_func(meta)
        giskard_test.meta = meta

        return giskard_test

    @classmethod
    def _read_meta_from_loca_dir(cls, uuid: str, project_key: Optional[str]) -> TestFunctionMeta:
        meta = tests_registry.get_test(uuid)
        if meta is None:
            assert f"Cannot find test function {uuid}"
        return meta

    def get_builder(self):
        return type(self)


Function = Callable[..., Result]

Test = Union[GiskardTest, Function]


class GiskardTestMethod(GiskardTest):
    params: ...

    def __init__(self, test_function: Function, **kwargs):
        self.params = kwargs
        test_uuid = get_test_uuid(test_function)
        meta = tests_registry.get_test(test_uuid)
        if meta is None:
            # equivalent to adding @test decorator
            test(test_function)
            meta = tests_registry.get_test(test_uuid)
        super(GiskardTest, self).__init__(test_function, meta)

    def execute(self) -> Result:
        return self.data(**self.params)

    def get_builder(self):
        return lambda **kwargs: GiskardTestMethod(self.data, **kwargs)
