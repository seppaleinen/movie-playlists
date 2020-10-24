package se.david.moviesimporter;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class Importer {
	@Value("${tmdb.api.url:https://api.themoviedb.org}")
	private String tmdbApiUrl;
	@Value("${tmdb.api.key}")
	private String apiKey;

	public void importMovie(String movieId) {
		String url = String.format("%s/3/movie/%s?api_key=%s&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images", tmdbApiUrl, movieId, apiKey);
	}

	public void importPerson(String personId) {
		String url = String.format("%s/3/person/%s?api_key=%s&language=en-USappend_to_response=images,movie_credits,external_ids", tmdbApiUrl, personId, apiKey);
	}

	public void importKeywords(String keywordId) {
		int page = 0;
		String url = String.format("%s/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=%s&with_keywords=%s", tmdbApiUrl, apiKey, page, keywordId);
	}
}
