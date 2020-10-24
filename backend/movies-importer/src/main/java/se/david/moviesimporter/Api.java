package se.david.moviesimporter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;
import se.david.moviesimporter.domain.Person;

@RestController
@RequestMapping(produces = MediaType.APPLICATION_JSON_VALUE)
public class Api {
	@Autowired
	private DailyImporter dailyImporter;
	@Autowired
	private Importer importer;

	@GetMapping(path = "/import/daily/production-companies", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> dailyFileOnProductionCompanies() {
		return dailyImporter.getProductionCompanyIds();
	}

	@GetMapping(path = "/import/daily/keyword-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> dailyFileOnKeywordIds() {
		return dailyImporter.getKeywordIds();
	}

	@GetMapping(path = "/import/daily/movie-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> dailyFileOnMovieIds() {
		return dailyImporter.getMovieIds();
	}

	@GetMapping(path = "/import/daily/person-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> dailyFileOnPersonIds() {
		return dailyImporter.getPersonIds();
	}

	@GetMapping(path = "/import/persons", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> fetchPersons() {
		return Flux.fromIterable(importer.findUnprocessedPersons())
				.parallel(5)
				.map(id -> importer.importPerson(id))
				.sequential();
	}

	@GetMapping(path = "/import/movies", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> fetchMovies() {
		return Flux.fromIterable(importer.findUnprocessedMovies())
				.parallel(5)
				.map(id -> importer.importMovie(id))
				.sequential();
	}

	@GetMapping(path = "/import/keywords", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> fetchKeywords() {
		return Flux.fromIterable(importer.findUnprocessedKeywords())
				.parallel(5)
				.map(id -> importer.importKeywords(id))
				.sequential();
	}
}
