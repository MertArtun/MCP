# WeatherMCP

FastMCP tabanlı basit bir hava durumu MCP sunucusu. Open-Meteo kullanır, API anahtarı gerekmez. `stdio` taşımacı ChatGPT MCP için, `http` taşımacı lokal/uzak test için uygundur.

## Kurulum
- Python 3.10+
- Bağımlılıklar: `fastmcp`, `httpx`
- Yükleme: `pip install fastmcp httpx` (veya `uv pip install fastmcp httpx`)

## Çalıştırma
- HTTP ile: `fastmcp run weather_server.py:mcp --transport http --port 8000`
- Stdio ile (ChatGPT MCP uyumlu): `fastmcp run weather_server.py:mcp`

## ChatGPT MCP entegrasyonu
`~/.mcp/servers/weather.json` örneği:
```json
{
  "command": ["fastmcp", "run", "/full/path/to/weather_server.py:mcp"],
  "transport": { "type": "stdio" },
  "name": "WeatherMCP"
}
```
ChatGPT ayarlarından Model Context Protocol → Add a server → bu dosyayı gösterin. Komut örnekleri:
- `get_weather_by_city city="Istanbul"`
- `get_weather lat=41.01 lon=28.97 unit="metric"`
- `get_forecast city="Hamburg" day_offset=1` (1=yarın, 0=bugün)

## Dosyalar
- `weather_server.py`: MCP sunucusu, `get_weather`, `get_weather_by_city`, `get_forecast` araçları.

## Notlar
- Open-Meteo ücretsiz ve anahtarsızdır; kota ve gecikme için istek başına 8s timeout tanımlıdır.
- İsteğe göre `fetch_weather` içine retry veya cache eklenebilir; ücretli servis anahtarı kullanmak isterseniz aynı yapı korunur, yalnızca HTTP isteğini değiştirmeniz yeterlidir.
