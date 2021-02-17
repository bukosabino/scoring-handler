import locust


class ApiUser(locust.HttpUser):
    wait_time = locust.constant_pacing(1)
    input_data = [5.1, 3.5, 1.4, 0.2]

    # @locust.task
    def health_check(self):
        self.client.get("/api/v1/healthcheck")

    # @locust.task
    def endpoint404(self):
        with self.client.get(
            "/api/v1/url_does_not_exist/", catch_response=True
        ) as response:
            if response.status_code == 404:
                response.success()


class ApiAsyncUser(ApiUser):

    url = "/api/v1/ml/async/predict"

    @locust.task
    def predict(self):
        self.client.post(self.url, json=self.input_data)


class ApiSyncUser(ApiUser):

    url = "/api/v1/ml/sync/predict"

    @locust.task
    def predict(self):
        self.client.post(self.url, json=self.input_data)
