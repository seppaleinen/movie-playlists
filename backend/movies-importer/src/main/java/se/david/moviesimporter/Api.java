package se.david.moviesimporter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Scheduler;
import reactor.core.scheduler.Schedulers;
import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;
import se.david.moviesimporter.domain.ProductionCompany;

@RestController
@RequestMapping(produces = MediaType.APPLICATION_JSON_VALUE)
public class Api {
	@Autowired
	private DailyImporter dailyImporter;

	@GetMapping(path = "/import/production-companies", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> productionCompanies() {
		return dailyImporter.getProductionCompanyIds();
	}

	@GetMapping(path = "/import/keyword-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> keywordIds() {
		return dailyImporter.getKeywordIds();
	}

	@GetMapping(path = "/import/movie-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> movieIds() {
		return dailyImporter.getMovieIds();
	}

	@GetMapping(path = "/import/person-ids", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	Flux<String> personIds() {
		return dailyImporter.getPersonIds();
	}
}
