import logging

import connexion


logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    app = connexion.FlaskApp(
        __name__, specification_dir=".", options={"swagger_ui": True}
    )
    app.add_api("daf-openapi.yaml")  # , validate_responses=True)
    app.run(port=8080)
