import json
import os
from datetime import datetime

from pyflink.common import Duration, Types, WatermarkStrategy
from pyflink.common.time import Time
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat
from pyflink.datastream.window import SlidingEventTimeWindows


def parse(line):
    event = json.loads(line)
    event["timestamp_ms"] = int(
        datetime.fromisoformat(event["event_time"].replace("Z", "+00:00")).timestamp() * 1000
    )
    return event


from pyflink.common.watermark_strategy import TimestampAssigner


class EventTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, event, record_timestamp):
        return event["timestamp_ms"]

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
source = FileSource.for_record_stream_format(
    StreamFormat.text_line_format(), os.getenv("EVENT_FILE", "/data/events.jsonl")
).monitor_continuously(Duration.of_seconds(2)).build()

events = env.from_source(source, WatermarkStrategy.no_watermarks(), "json-file").map(parse)
watermarks = WatermarkStrategy.for_bounded_out_of_orderness(
    Duration.of_seconds(10)
).with_timestamp_assigner(EventTimestampAssigner())

alerts = (
    events.assign_timestamps_and_watermarks(watermarks)
    .filter(lambda event: event["event_type"] == "click")
    .map(lambda event: (event["product_id"], 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
    .key_by(lambda item: item[0])
    .window(SlidingEventTimeWindows.of(Time.minutes(1), Time.seconds(20)))
    .reduce(lambda left, right: (left[0], left[1] + right[1]))
    .filter(lambda item: item[1] >= int(os.getenv("TREND_THRESHOLD", "5")))
)

# Primeiro checkpoint: saída no console. Na integração, este resultado será
# enviado ao HBase por REST/Thrift para evitar dependências Java no PyFlink.
alerts.print("ALERTA_PRODUTO_EM_ALTA")
env.execute("ecommerce-trending-products")
