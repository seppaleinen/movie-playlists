package se.david.moviesimporter.repository;

import java.util.List;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Movie;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
	@Transactional
	default List<Movie> saveAllWithTransaction(List<Movie> movies){
		return saveAll(movies);
	}
}
