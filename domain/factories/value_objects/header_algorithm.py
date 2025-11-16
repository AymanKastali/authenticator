from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo


class JwtHeaderAlgorithmVoFactory:
    @classmethod
    def from_string(cls, algorithm_str: str) -> JwtHeaderAlgorithmVo:
        algorithm_str = algorithm_str.strip().upper()
        return JwtHeaderAlgorithmVo[algorithm_str]
