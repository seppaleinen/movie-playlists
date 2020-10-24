package se.david.moviesimporter;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;
import se.david.moviesimporter.domain.ProductionCompany;
import se.david.moviesimporter.repository.KeywordRepository;
import se.david.moviesimporter.repository.MovieRepository;
import se.david.moviesimporter.repository.PersonRepository;
import se.david.moviesimporter.repository.ProductionCompanyRepository;
import se.david.moviesimporter.util.RestTemplateFetcher;

@Service
public class Importer {
	@Value("${tmdb.api.url:https://api.themoviedb.org}")
	private String tmdbApiUrl;
	@Value("${tmdb.api.key}")
	private String apiKey;

	@Autowired
	private PersonRepository personRepository;
	@Autowired
	private KeywordRepository keywordRepository;
	@Autowired
	private MovieRepository movieRepository;
	@Autowired
	private ProductionCompanyRepository productionCompanyRepository;

	public String importMovie(long movieId) {
		String url = String.format("%s/3/movie/%s?api_key=%s&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images", tmdbApiUrl, movieId, apiKey);
		try {
			Optional<Movie> result = RestTemplateFetcher.fetchMovie(url);
			if(result.isPresent()) {
				movieRepository.setToProcessed(movieId);
			} else {
				movieRepository.deleteByIdWithTransaction(movieId);
			}
			return "Done";
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

	public String importPerson(long personId) {
		String url = String.format("%s/3/person/%s?api_key=%s&language=en-USappend_to_response=images,movie_credits,external_ids", tmdbApiUrl, personId, apiKey);
		try {
			Optional<Person> result = RestTemplateFetcher.fetchPerson(url);
			if(result.isPresent()) {
				personRepository.setToProcessed(personId);
			} else {
				personRepository.deleteByIdWithTransaction(personId);
			}
			return "Done";
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

	public String importKeywords(long keywordId) {
		int page = 1;
		String url = String.format("%s/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=%s&with_keywords=%s", tmdbApiUrl, apiKey, page, keywordId);
		try {
			Optional<Keyword> result = RestTemplateFetcher.fetchKeyword(url);
			if(result.isPresent()) {
				keywordRepository.setToProcessed(keywordId);
			} else {
				keywordRepository.deleteByIdWithTransaction(keywordId);
			}
			return "Done";
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

	public List<Long> findUnprocessedPersons() {
		return personRepository.findAllUnprocessed();
	}

	public List<Long> findUnprocessedKeywords() {
		return keywordRepository.findAllUnprocessed();
	}

	public List<Long> findUnprocessedMovies() {
		return movieRepository.findAllUnprocessed();
	}
}
