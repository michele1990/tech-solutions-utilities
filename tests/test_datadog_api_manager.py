# src/datadog_client.py
from datadog_api_client import Configuration, AsyncApiClient
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.exceptions import ApiException
from aiosonic.exceptions import ConnectTimeout
import asyncio
from datetime import datetime, timedelta
import logging
from .logging_helper import format_log_message

class DatadogClient:
    def __init__(self, api_key, app_key, timeout, max_retries, backoff_factor, query_template):
        self.api_key = api_key
        self.app_key = app_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.query_template = query_template
        self.configuration = Configuration()
        self.configuration.api_key['apiKeyAuth'] = api_key
        self.configuration.api_key['appKeyAuth'] = app_key

    def create_query(self, store_address_id):
        return self.query_template.format(store_address_id=store_address_id)

    async def fetch_logs(self, store_address_id, semaphore, time_range_minutes=10080, limit=1000):
        logging.info(format_log_message("preparing_fetch", store_address_id=store_address_id))
        attempts = 0
        now = datetime.utcnow()
        from_time = now - timedelta(minutes=time_range_minutes)
        to_time = now

        query = LogsListRequest(
            query=self.create_query(store_address_id),
            limit=limit,
            time={
                'from': from_time.isoformat() + "Z",
                'to': to_time.isoformat() + "Z"
            }
        )

        async with semaphore:
            while attempts < self.max_retries:
                try:
                    async with AsyncApiClient(self.configuration) as api_client:
                        api_instance = LogsApi(api_client)
                        logging.info(format_log_message("api_request_sent", store_address_id=store_address_id))
                        response = await asyncio.wait_for(api_instance.list_logs(body=query), self.timeout)
                        logging.info(format_log_message("api_response_received", store_address_id=store_address_id))
                        return response
                except (ApiException, ConnectTimeout, asyncio.TimeoutError) as e:
                    attempts += 1
                    logging.warning(format_log_message("retry_warning", attempt=attempts, error=str(e), store_address_id=store_address_id))
                    if attempts >= self.max_retries:
                        logging.error(format_log_message("final_error", store_address_id=store_address_id, error=str(e)))
                        return None
                    sleep_time = self.backoff_factor * (2 ** attempts)
                    logging.info(format_log_message("retry_info", sleep_time=sleep_time, store_address_id=store_address_id))
                    await asyncio.sleep(sleep_time)
                except Exception as e:
                    logging.error(format_log_message("unexpected_error", store_address_id=store_address_id, error=str(e)))
                    attempts += 1
                    if attempts >= self.max_retries:
                        logging.error(format_log_message("all_attempts_failed_unexpected", store_address_id=store_address_id, error=str(e)))
                        return None
                    sleep_time = self.backoff_factor * (2 ** attempts)
                    logging.info(format_log_message("retry_info", sleep_time=sleep_time, store_address_id=store_address_id))
                    await asyncio.sleep(sleep_time)

            logging.error(format_log_message("exiting_due_to_failures", store_address_id=store_address_id))
            return None

