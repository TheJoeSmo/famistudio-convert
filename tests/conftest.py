from logging import DEBUG, basicConfig

basicConfig(filename="tests/test.log", level=DEBUG, encoding="utf-8", filemode="w")

import famistudio_convert  # noqa: F401, E402
