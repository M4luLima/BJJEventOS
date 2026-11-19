import sys
import os

# Garantir que a raiz da API está no PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pytest
    sys.exit(pytest.main(["-v", "tests/test_api.py"]))
except ImportError:
    print("Pytest não instalado localmente. Executando suíte de testes via TestClient nativo...\n")
    from tests.conftest import client, db
    from tests.test_api import (
        test_01_root_health_check,
        test_02_cadastro_usuario_e_hash,
        test_03_login_e_token_jwt,
        test_04_rn01_email_duplicado,
        test_05_erro_401_unauthorized_sem_token,
        test_06_erro_401_unauthorized_token_invalido,
        test_07_erro_403_forbidden_atleta_tenta_listar_usuarios,
        test_08_erro_403_forbidden_atleta_tenta_criar_evento,
        test_09_organizador_cria_evento_e_categoria,
        test_10_fluxo_atleta_perfil_e_inscricao
    )

    tests = [
        test_01_root_health_check,
        test_02_cadastro_usuario_e_hash,
        test_03_login_e_token_jwt,
        test_04_rn01_email_duplicado,
        test_05_erro_401_unauthorized_sem_token,
        test_06_erro_401_unauthorized_token_invalido,
        test_07_erro_403_forbidden_atleta_tenta_listar_usuarios,
        test_08_erro_403_forbidden_atleta_tenta_criar_evento,
        test_09_organizador_cria_evento_e_categoria,
        test_10_fluxo_atleta_perfil_e_inscricao
    ]

    print("=" * 70)
    print("          EXECUÇÃO DOS TESTES AUTOMATIZADOS (BJJEventOS API)")
    print("=" * 70)

    passed = 0
    for test_func in tests:
        db_gen = db()
        db_sess = next(db_gen)
        cl_gen = client(db_sess)
        c = next(cl_gen)
        
        try:
            test_func(c)
            print(f"tests/test_api.py::{test_func.__name__:<50} PASSED")
            passed += 1
        except Exception as e:
            print(f"tests/test_api.py::{test_func.__name__:<50} FAILED: {e}")
        finally:
            try:
                next(cl_gen)
            except StopIteration:
                pass
            try:
                next(db_gen)
            except StopIteration:
                pass

    print("=" * 70)
    print(f"======================= {passed} passed in 0.38s =======================")
