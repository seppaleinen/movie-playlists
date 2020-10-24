package se.david.moviesimporter.util;

import static org.slf4j.LoggerFactory.getLogger;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Optional;

import org.apache.http.impl.client.HttpClientBuilder;
import org.slf4j.Logger;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.util.StreamUtils;
import org.springframework.web.client.RestTemplate;

import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;

public final class RestTemplateFetcher {
	private static final Logger log = getLogger(RestTemplateFetcher.class);

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

	public static Optional<Movie> fetchMovie(String url) throws IOException {
		try {
			ResponseEntity<Movie> response = restTemplate.getForEntity(url, Movie.class);
			if (response.getStatusCode().is2xxSuccessful() && response.hasBody()) {
				return Optional.ofNullable(response.getBody());
			} else if (response.getStatusCode() == HttpStatus.NOT_FOUND) {
				return Optional.empty();
			} else {
				log.error("Unknown error code: {} when calling: {}", response.getStatusCode(), url);
				throw new IOException("Error handling url=" + url);
			}
		} catch (Exception e) {
			log.error("Something went wrong: {}", e.getMessage(), e);
			throw new IOException("Could not call " + url, e);
		}
	}

	public static Optional<Keyword> fetchKeyword(String url) throws IOException {
		try {
			ResponseEntity<Keyword> response = restTemplate.getForEntity(url, Keyword.class);
			if (response.getStatusCode().is2xxSuccessful() && response.hasBody()) {
				return Optional.ofNullable(response.getBody());
			} else if (response.getStatusCode() == HttpStatus.NOT_FOUND) {
				return Optional.empty();
			} else {
				log.error("Unknown error code: {} when calling: {}", response.getStatusCode(), url);
				throw new IOException("Error handling url=" + url);
			}
		} catch (Exception e) {
			log.error("Something went wrong: {}", e.getMessage(), e);
			throw new IOException("Could not call " + url, e);
		}
	}

	public static Optional<Person> fetchPerson(String url) throws IOException {
		try {
			ResponseEntity<Person> response = restTemplate.getForEntity(url, Person.class);
			if (response.getStatusCode().is2xxSuccessful() && response.hasBody()) {
				return Optional.ofNullable(response.getBody());
			} else if (response.getStatusCode() == HttpStatus.NOT_FOUND) {
				return Optional.empty();
			} else {
				log.error("Unknown error code: {} when calling: {}", response.getStatusCode(), url);
				throw new IOException("Error handling url=" + url);
			}
		} catch (Exception e) {
			log.error("Something went wrong: {}", e.getMessage(), e);
			throw new IOException("Could not call " + url, e);
		}
	}
}
