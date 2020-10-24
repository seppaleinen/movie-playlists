package se.david.moviesimporter.repository;

import java.util.List;
import java.util.stream.Stream;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Movie;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
	@Transactional
	default List<Movie> saveAllWithTransaction(List<Movie> movies) {
		return saveAll(movies);
	}

	@Transactional
	@Query(value = "select m.id from Movie m where m.processed = false")
	List<Long> findAllUnprocessed();

	@Transactional
	@Modifying
	@Query("update Movie m set m.processed = true where m.id = ?1")
	void setToProcessed(long id);

	@Transactional
	@Modifying
	default void deleteByIdWithTransaction(long id) {
		deleteById(id);
	}
}
