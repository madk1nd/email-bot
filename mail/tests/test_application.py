from unittest import mock


def test_main():
    with mock.patch('api.application.logging') as logger:
        with mock.patch('api.application.TOKEN'):
            with mock.patch('api.application.web') as web:
                with mock.patch('api.application.MongoClient') as client:
                    with mock.patch('api.application.setup_swagger') as swagger:
                        with mock.patch('api.application.Dispatcher') as dispatcher:
                            from api.application import main
                            main()
