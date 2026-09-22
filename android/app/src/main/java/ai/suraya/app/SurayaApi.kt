package ai.suraya.app

import java.net.HttpURLConnection
import java.net.URL

data class ApiResult(
    val success: Boolean,
    val body: String,
    val error: String? = null,
)

class SurayaApi(
    private val baseUrl: String,
) {

    fun health(): ApiResult {
        return get("/health")
    }

    fun status(): ApiResult {
        return get("/status")
    }

    fun command(command: String): ApiResult {
        return post(
            path = "/command",
            body = """
                {
                    "command": ${jsonString(command)}
                }
            """.trimIndent(),
        )
    }

    private fun get(path: String): ApiResult {
        return request(
            method = "GET",
            path = path,
        )
    }

    private fun post(
        path: String,
        body: String,
    ): ApiResult {
        return request(
            method = "POST",
            path = path,
            body = body,
        )
    }

    private fun request(
        method: String,
        path: String,
        body: String? = null,
    ): ApiResult {
        return try {
            val url = URL(
                baseUrl.trimEnd('/') + path
            )

            val connection =
                url.openConnection() as HttpURLConnection

            connection.requestMethod = method
            connection.connectTimeout = 10_000
            connection.readTimeout = 30_000
            connection.setRequestProperty(
                "Content-Type",
                "application/json",
            )

            if (body != null) {
                connection.doOutput = true

                connection.outputStream.use { stream ->
                    stream.write(
                        body.toByteArray(
                            Charsets.UTF_8
                        )
                    )
                }
            }

            val status = connection.responseCode

            val stream =
                if (status in 200..299) {
                    connection.inputStream
                } else {
                    connection.errorStream
                }

            val responseBody =
                stream?.bufferedReader()?.use {
                    it.readText()
                } ?: ""

            ApiResult(
                success = status in 200..299,
                body = responseBody,
                error = if (status !in 200..299) {
                    "HTTP $status"
                } else {
                    null
                },
            )
        } catch (exception: Exception) {
            ApiResult(
                success = false,
                body = "",
                error = exception.message
                    ?: "Network error",
            )
        }
    }

    private fun jsonString(value: String): String {
        return buildString {
            append('"')

            value.forEach { character ->
                when (character) {
                    '\\' -> append("\\\\")
                    '"' -> append("\\\"")
                    '\n' -> append("\\n")
                    '\r' -> append("\\r")
                    '\t' -> append("\\t")
                    else -> append(character)
                }
            }

            append('"')
        }
    }
}
