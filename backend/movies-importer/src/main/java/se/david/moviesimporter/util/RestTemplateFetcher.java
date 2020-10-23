package se.david.moviesimporter.util;

import java.io.File;
import java.io.FileOutputStream;

import org.apache.http.impl.client.HttpClientBuilder;
import org.springframework.http.HttpMethod;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.util.StreamUtils;
import org.springframework.web.client.RestTemplate;

public final class RestTemplateFetcher {
	private static final RestTemplate restTemplate = new RestTemplate(new HttpComponentsClientHttpRequestFactory(
			HttpClientBuilder.create().build()));

	private RestTemplateFetcher() {
	}

	public static File downloadFile(String url) {
		return restTemplate.execute(url, HttpMethod.GET, null, clientHttpResponse -> {
			File tmpfile = File.createTempFile("download", "temp");
			StreamUtils.copy(clientHttpResponse.getBody(), new FileOutputStream(tmpfile));
			return tmpfile;
		});
	}
}
