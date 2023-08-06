from typing import List, Optional

from aws_cdk.aws_lambda import Runtime
from aws_cdk.core import Stack
from b_cfn_lambda_layer.lambda_layer import LambdaLayer


class OpensearchIndexLayer(LambdaLayer):
    def __init__(
        self,
        scope: Stack,
        name: str
    ) -> None:
        super().__init__(
            scope=scope,
            name=name,
            source_path=self.source_path(),
            code_runtimes=self.runtimes()

        )

    @staticmethod
    def source_path() -> str:
        from . import root
        return root

    @staticmethod
    def runtimes() -> Optional[List[Runtime]]:
        return [Runtime.PYTHON_3_8]
