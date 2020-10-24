package se.david.moviesimporter;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.stubFor;
import static com.github.tomakehurst.wiremock.client.WireMock.verify;

import java.io.IOException;
import java.nio.file.Files;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.contract.wiremock.AutoConfigureWireMock;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;

import com.github.tomakehurst.wiremock.client.WireMock;

@SpringBootTest(
		webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
		classes = MoviesImporterApplication.class)
@ExtendWith(SpringExtension.class)
@AutoConfigureWireMock(port = 9999)
class MoviesDailyImporterApplicationTests {
	@Autowired
	private WebTestClient webClient;

	@Test
	void importProductionCompanies() throws IOException {
		ClassPathResource resource = new ClassPathResource("production_companies.json.gz");

		String url = "/p/exports/production_company_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/production-companies")
				.exchange()
				.expectStatus().is2xxSuccessful();

		verify(WireMock.getRequestedFor(WireMock.urlMatching(url)));
	}

	@Test
	void importProductionCompaniesTwice() throws IOException {
		ClassPathResource resource = new ClassPathResource("production_companies.json.gz");

		String url = "/p/exports/production_company_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/production-companies")
				.exchange()
				.expectStatus().is2xxSuccessful();

		webClient.get().uri("/import/production-companies")
				.exchange()
				.expectStatus().is2xxSuccessful();
	}

	@Test
	void importKeywordIds() throws IOException {
		ClassPathResource resource = new ClassPathResource("keywords.json.gz");

		String url = "/p/exports/keyword_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/keyword-ids")
				.exchange()
				.expectStatus().is2xxSuccessful();

		verify(WireMock.getRequestedFor(WireMock.urlMatching(url)));
	}

	@Test
	void importKeywordIdsTwice() throws IOException {
		ClassPathResource resource = new ClassPathResource("keywords.json.gz");

		String url = "/p/exports/keyword_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/keyword-ids")
				.exchange()
				.expectStatus().is2xxSuccessful();

		webClient.get().uri("/import/keyword-ids")
				.exchange()
				.expectStatus().is2xxSuccessful();

		verify(WireMock.getRequestedFor(WireMock.urlMatching(url)));
	}

	@Test
	void importMovieIds() throws IOException {
		ClassPathResource resource = new ClassPathResource("movies.json.gz");

		String url = "/p/exports/movie_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/movie-ids")
				.exchange()
				.expectStatus().is2xxSuccessful();

		verify(WireMock.getRequestedFor(WireMock.urlMatching(url)));
	}

	@Test
	void importPersonIds() throws IOException {
		ClassPathResource resource = new ClassPathResource("persons.json.gz");

		String url = "/p/exports/person_ids_.*.json.gz";
		stubEndpoint(resource, url);

		webClient.get().uri("/import/person-ids")
				.exchange()
				.expectStatus().is2xxSuccessful();

		verify(WireMock.getRequestedFor(WireMock.urlMatching(url)));
	}

	private void stubEndpoint(ClassPathResource resource, String url) throws IOException {
		stubFor(WireMock.get(WireMock.urlMatching(url)).willReturn(
				aResponse()
						.withHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_OCTET_STREAM_VALUE)
						.withBody(Files.readAllBytes(resource.getFile().toPath())))
		);
	}

}
