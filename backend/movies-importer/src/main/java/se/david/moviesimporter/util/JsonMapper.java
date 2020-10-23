package se.david.moviesimporter.util;

import static org.slf4j.LoggerFactory.getLogger;

import java.util.function.Function;

import org.slf4j.Logger;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import se.david.moviesimporter.domain.Keyword;
import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;
import se.david.moviesimporter.domain.ProductionCompany;

public final class JsonMapper {
	private static final Logger log = getLogger(JsonMapper.class);
	private static final ObjectMapper objectMapper = new ObjectMapper();

	private JsonMapper() {
	}

	public static Function<String, ProductionCompany> mapProductionCompany() {
		return content -> {
			try {
				return objectMapper.readValue(content, ProductionCompany.class);
			} catch (JsonProcessingException e) {
				log.error("Error: {}", e.getMessage(), e);
				return null;
			}
		};
	}

	public static Function<String, Person> mapPerson() {
		return content -> {
			try {
				return objectMapper.readValue(content, Person.class);
			} catch (JsonProcessingException e) {
				log.error("Error: {}", e.getMessage(), e);
				return null;
			}
		};
	}

	public static Function<String, Movie> mapMovie() {
		return content -> {
			try {
				return objectMapper.readValue(content, Movie.class);
			} catch (JsonProcessingException e) {
				log.error("Error: {}", e.getMessage(), e);
				return null;
			}
		};
	}

	public static Function<String, Keyword> mapKeyword() {
		return content -> {
			try {
				return objectMapper.readValue(content, Keyword.class);
			} catch (JsonProcessingException e) {
				log.error("Error: {}", e.getMessage(), e);
				return null;
			}
		};
	}
}
