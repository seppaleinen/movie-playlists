package se.david.moviesimporter;

import static org.slf4j.LoggerFactory.getLogger;

import java.io.File;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Objects;

import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import reactor.core.publisher.Flux;
import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;
import se.david.moviesimporter.domain.ProductionCompany;
import se.david.moviesimporter.repository.KeywordRepository;
import se.david.moviesimporter.repository.MovieRepository;
import se.david.moviesimporter.repository.PersonRepository;
import se.david.moviesimporter.repository.ProductionCompanyRepository;
import se.david.moviesimporter.util.FileReader;
import se.david.moviesimporter.util.JsonMapper;
import se.david.moviesimporter.util.RestTemplateFetcher;

/*
 * https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US
 */
@Service
public class Importer {
	private static final Logger log = getLogger(Importer.class);
	private static final DateTimeFormatter datetimeFormatter = DateTimeFormatter.ofPattern("MM_dd_yyyy");

	private final LocalDate localDate;
	private final KeywordRepository keywordRepository;
	private final MovieRepository movieRepository;
	private final PersonRepository personRepository;
	private final ProductionCompanyRepository productionCompanyRepository;

	@Value("${tmdb.files.url:http://files.tmdb.org}")
	private String tmdbFilesUrl;

	@Autowired
	public Importer(KeywordRepository keywordRepository,
			MovieRepository movieRepository,
			PersonRepository personRepository,
			ProductionCompanyRepository productionCompanyRepository) {
		this.localDate = LocalDate.now(ZoneId.of("Europe/Stockholm")).minusDays(1);
		this.keywordRepository = keywordRepository;
		this.movieRepository = movieRepository;
		this.personRepository = personRepository;
		this.productionCompanyRepository = productionCompanyRepository;
	}

	public Flux<ProductionCompany> getProductionCompanyIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/production_company_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapProductionCompany())
				.filter(Objects::nonNull)
				.buffer(100)
				.flatMap(productionCompanies -> Flux.fromIterable(productionCompanyRepository.saveAll(productionCompanies)))
				.log();
	}

	public Flux<Keyword> getKeywordIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/keyword_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapKeyword())
				.filter(Objects::nonNull)
				.buffer(100)
				.flatMap(keywords -> Flux.fromIterable(keywordRepository.saveAll(keywords)))
				.log();
	}

	public Flux<Person> getPersonIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/person_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapPerson())
				.filter(Objects::nonNull)
				.filter(person -> !person.isAdult())
				.buffer(100)
				.flatMap(persons -> Flux.fromIterable(personRepository.saveAll(persons)))
				.log();
	}

	public Flux<Movie> getMovieIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/movie_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapMovie())
				.filter(Objects::nonNull)
				.filter(movie -> !movie.isAdult())
				.buffer(100)
				.flatMap(movies -> Flux.fromIterable(movieRepository.saveAll(movies)), 5)
				.log();
	}
}
