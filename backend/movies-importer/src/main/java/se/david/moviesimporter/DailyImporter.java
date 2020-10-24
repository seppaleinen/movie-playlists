package se.david.moviesimporter;

import static org.slf4j.LoggerFactory.getLogger;

import java.io.File;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

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
public class DailyImporter {
	private static final Logger log = getLogger(DailyImporter.class);
	private static final DateTimeFormatter datetimeFormatter = DateTimeFormatter.ofPattern("MM_dd_yyyy");

	private final LocalDate localDate;
	private final KeywordRepository keywordRepository;
	private final MovieRepository movieRepository;
	private final PersonRepository personRepository;
	private final ProductionCompanyRepository productionCompanyRepository;

	@Value("${tmdb.files.url:http://files.tmdb.org}")
	private String tmdbFilesUrl;

	@Autowired
	public DailyImporter(KeywordRepository keywordRepository,
			MovieRepository movieRepository,
			PersonRepository personRepository,
			ProductionCompanyRepository productionCompanyRepository) {
		this.localDate = LocalDate.now(ZoneId.of("Europe/Stockholm")).minusDays(1);
		this.keywordRepository = keywordRepository;
		this.movieRepository = movieRepository;
		this.personRepository = personRepository;
		this.productionCompanyRepository = productionCompanyRepository;
	}

	public Flux<String> getProductionCompanyIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/production_company_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		log.info("File downloaded");

		AtomicInteger counter = new AtomicInteger();

		int buffer = 100;
		return Flux.fromStream(FileReader.readFile(file))
				.map(JsonMapper.mapProductionCompany())
				.filter(Objects::nonNull)
				.buffer(buffer)
				.map(a -> {
					List<ProductionCompany> found = productionCompanyRepository.findAllById(a.stream().map(ProductionCompany::getId).collect(Collectors.toList()));
					return a.stream()
							.filter(b -> !found.contains(b))
							.collect(Collectors.toList());
				})
				.flatMap(productionCompanies -> Flux.fromIterable(productionCompanyRepository.saveAllWithTransaction(productionCompanies)))
				.buffer(buffer)
				.filter(a -> counter.addAndGet(buffer) % 10_000 == 0)
				.map(a -> String.format("Processed: %s", counter.get()))
				.doOnNext(a -> log.info("Processed: {} production companies", counter.get()));
	}

	public Flux<String> getKeywordIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/keyword_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		log.info("File downloaded");

		AtomicInteger counter = new AtomicInteger();

		int buffer = 100;
		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapKeyword())
				.filter(Objects::nonNull)
				.buffer(buffer)
				.map(a -> {
					List<Keyword> found = keywordRepository.findAllById(a.stream().map(Keyword::getId).collect(Collectors.toList()));
					return a.stream()
							.filter(b -> !found.contains(b))
							.collect(Collectors.toList());
				})
				.flatMap(keywords -> Flux.fromIterable(keywordRepository.saveAllWithTransaction(keywords)))
				.buffer(buffer)
				.filter(a -> counter.addAndGet(buffer) % 10_000 == 0)
				.map(a -> String.format("Processed: %s", counter.get()))
				.doOnNext(a -> log.info("Processed: {} keywords", counter.get()));
	}

	public Flux<String> getPersonIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/person_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		log.info("File downloaded");

		AtomicInteger counter = new AtomicInteger();

		int buffer = 100;
		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapPerson())
				.filter(Objects::nonNull)
				.filter(person -> !person.isAdult())
				.buffer(buffer)
				.map(a -> {
					List<Person> found = personRepository.findAllById(a.stream().map(Person::getId).collect(Collectors.toList()));
					return a.stream()
							.filter(b -> !found.contains(b))
							.collect(Collectors.toList());
				})
				.flatMap(persons -> Flux.fromIterable(personRepository.saveAllWithTransaction(persons)))
				.buffer(buffer)
				.filter(a -> counter.addAndGet(buffer) % 10_000 == 0)
				.map(a -> String.format("Processed: %s", counter.get()))
				.doOnNext(a -> log.info("Processed: {} persons", counter.get()));
	}

	public Flux<String> getMovieIds() {
		String date = datetimeFormatter.format(localDate);
		String url = String.format("%s/p/exports/movie_ids_%s.json.gz", tmdbFilesUrl, date);
		File file = RestTemplateFetcher.downloadFile(url);

		log.info("File downloaded");

		AtomicInteger counter = new AtomicInteger();

		int buffer = 1000;
		return Flux.fromStream(FileReader.readFile(file))
				.onBackpressureBuffer()
				.map(JsonMapper.mapMovie())
				.filter(Objects::nonNull)
				.filter(movie -> !movie.isAdult())
				.buffer(buffer)
				.map(a -> {
					List<Movie> found = movieRepository.findAllById(a.stream().map(Movie::getId).collect(Collectors.toList()));
					return a.stream()
							.filter(b -> !found.contains(b))
							.collect(Collectors.toList());
				})
				.flatMap(movies -> Flux.fromIterable(movieRepository.saveAllWithTransaction(movies)), 5)
				.buffer(buffer)
				.filter(a -> counter.addAndGet(buffer) % 10_000 == 0)
				.map(movie -> String.format("Processed: %s", counter.get()))
				.doOnNext(a -> log.info("Processed: {} movies", counter.get()));
	}
}
