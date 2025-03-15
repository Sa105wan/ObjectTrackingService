

class LogEntry:
    def __init__(self, service_name, ip_address, location, grpc_system_response_time,
                 grpc_system_latency, total_response_time, total_latency):
        self._service_name = service_name
        self._ip_address = ip_address
        self._location = location
        self._grpc_system_response_time = grpc_system_response_time
        self._grpc_system_latency = grpc_system_latency
        self._total_response_time = total_response_time
        self._total_latency = total_latency

    @property
    def service_name(self):
        return self._service_name

    @service_name.setter
    def service_name(self, value):
        self._service_name = value

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def grpc_system_response_time(self):
        return self._grpc_system_response_time

    @grpc_system_response_time.setter
    def grpc_system_response_time(self, value):
        self._grpc_system_response_time = value

    @property
    def grpc_system_latency(self):
        return self._grpc_system_latency

    @grpc_system_latency.setter
    def grpc_system_latency(self, value):
        self._grpc_system_latency = value

    @property
    def total_response_time(self):
        return self._total_response_time

    @total_response_time.setter
    def total_response_time(self, value):
        self._total_response_time = value

    @property
    def total_latency(self):
        return self._total_latency

    @total_latency.setter
    def total_latency(self, value):
        self._total_latency = value
