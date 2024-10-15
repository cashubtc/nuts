# NUT-XX: HTTP Compression

`optional`

---

This NUT specifies that the communication with the mint should use HTTP compression.

For compression to be used between a wallet and a mint, both the wallet (HTTP client) and the mint (HTTP server) have to support it.

## Mints

Mints that implement this NUT support HTTP compression for all exposed REST endpoints. This can be done natively by the mint, or externally, for example through a reverse proxy.

If the mint software package supports compression natively, it must offer a configuration option by which the mint operator can enable or disable compression support. This option should be enabled by default.

If the mint doesn't support it natively, the mint documentation must include instructions on the deployment options available to mint operators that support HTTP compression, for example using an nginx reverse proxy.

Using one of the two options above, the mint should support as many compression algorithms as possible. At a minimum, gzip and deflate must be supported.

## Wallets

Wallets that implement this NUT must ensure the compression header is set in their HTTP requests to the mint. This must be done regardless if the mint signals support for this NUT, as a mint can inadvertently support it through a reverse proxy.

The wallet should support as many compression algorithms as possible. At a minimum, it must support gzip or deflate.

The compression header must contain all compression algorithms supported by the wallet, listed in the order of preference, for example:
```
Accept-Encoding: br, gzip, deflate
```


## Comparison

Below is a comparison of popular HTTP compression algorithms. It looks at a typical mint's keyset response[^1] and how each algorithm affects its payload size and transfer time over mobile networks:


| Compression | Payload[^1] (bytes) | LTE[^2] (ms) | 4G[^2] (ms) | 3G[^2] (ms) | 2G[^2] (ms) |
|-------------|--------------------:|-------------:|------------:|------------:|------------:|
| none        |                5309 |         0.85 |        2.12 |       28.30 |      424.80 |
| gzip        |                3014 |         0.48 |        1.21 |       16.01 |      241.20 |
| deflate     |                3002 |         0.48 |        1.20 |       16.00 |      240.20 |
| brotli      |                2749 |         0.44 |        1.10 |       14.70 |      219.60 |
| zstd        |                2737 |         0.44 |        1.09 |       14.60 |      219.00 |

The 4G and LTE values are a good reference point for mobile wallets.

The 2G and 3G[^5] values are more relevant for IoT devices[^4], mobile devices with degraded coverage (for example merchants in remote areas) or mobile wallet usage in developing countries[^3].



[^1]: Response body size for `/v1/keys/{keyset_id}` using a standard setup of 64 pubkeys for amounts that are powers of two

[^2]: Transfer times calculated based on average speeds: 0.1 Mbps for 2G, 1.5 Mbps for 3G, 20 Mbps for 4G, 50 Mbps for LTE

[^3]: In the least developed parts of the world, ~1/3 of the population use 2G and 3G, as per https://www.itu.int/itu-d/reports/statistics/2023/10/10/ff23-mobile-network-coverage/ .

[^4]: 2G and 3G modules are commonly used IoT devices because they are cheaper.

[^5]: 2G and 3G networks are being slowly phased out. In Europe, this is expected to last until at least 2030. See last page of the [Report on practices and challenges of the
phasing out of 2G and 3G](https://www.berec.europa.eu/system/files/2023-12/BoR%20%2823%29%20204%20BEREC%20Report%20on%20practices%20and%20challenges%20of%20the%20phasing%20out%20of%202G%20and%203G_0.pdf)