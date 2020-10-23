package se.david.moviesimporter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;
import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;
import se.david.moviesimporter.domain.ProductionCompany;

@RestController
@RequestMapping(produces = MediaType.APPLICATION_JSON_VALUE)
public class Api {
	@Autowired
	private Importer importer;

	@GetMapping(path = "/import/production-companies")
	Flux<ProductionCompany> productionCompanies() {
		return importer.getProductionCompanyIds();
	}

	@GetMapping(path = "/import/keyword-ids")
	Flux<Keyword> keywordIds() {
		return importer.getKeywordIds();
	}

	@GetMapping(path = "/import/movie-ids")
	Flux<Movie> movieIds() {
		return importer.getMovieIds();
	}

	@GetMapping(path = "/import/person-ids")
	Flux<Person> personIds() {
		return importer.getPersonIds();
	}
}
