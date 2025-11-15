from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo


class JwtHeaderAlgorithmVoFactory:
    @classmethod
    def from_string(cls, algorithm_str: str) -> JwtHeaderAlgorithmVo:
        return JwtHeaderAlgorithmVo(algorithm_str.strip().upper())
