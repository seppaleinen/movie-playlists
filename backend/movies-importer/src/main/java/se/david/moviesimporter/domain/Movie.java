package se.david.moviesimporter.domain;

import java.util.Objects;

import javax.persistence.Entity;
import javax.persistence.Id;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * {"adult":false,"id":3924,"original_title":"Blondie","popularity":2.405,"video":false}
 */
@Entity
public class Movie {
	@Id
	private long id;
	private boolean adult;
	@JsonProperty("original_title")
	private String originalTitle;
	private double popularity;
	private boolean video;

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public boolean isAdult() {
		return adult;
	}

	public void setAdult(boolean adult) {
		this.adult = adult;
	}

	public String getOriginalTitle() {
		return originalTitle;
	}

	public void setOriginalTitle(String originalTitle) {
		this.originalTitle = originalTitle;
	}

	public double getPopularity() {
		return popularity;
	}

	public void setPopularity(double popularity) {
		this.popularity = popularity;
	}

	public boolean isVideo() {
		return video;
	}

	public void setVideo(boolean video) {
		this.video = video;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) {
			return true;
		}
		if (o == null || getClass() != o.getClass()) {
			return false;
		}
		Movie movie = (Movie) o;
		return id == movie.id &&
				adult == movie.adult &&
				Double.compare(movie.popularity, popularity) == 0 &&
				video == movie.video &&
				Objects.equals(originalTitle, movie.originalTitle);
	}

	@Override
	public int hashCode() {
		return Objects.hash(id, adult, originalTitle, popularity, video);
	}

	@Override
	public String toString() {
		return "Movie{" +
				"id=" + id +
				", adult=" + adult +
				", originalTitle='" + originalTitle + '\'' +
				", popularity=" + popularity +
				", video=" + video +
				'}';
	}
}
