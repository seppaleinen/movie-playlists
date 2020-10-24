package se.david.moviesimporter.repository;

import java.util.List;
import java.util.stream.Stream;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Keyword;

@Repository
public interface KeywordRepository extends JpaRepository<Keyword, Long> {
	@Transactional
	default List<Keyword> saveAllWithTransaction(List<Keyword> keywords) {
		return saveAll(keywords);
	}

	@Transactional
	@Query(value = "select k.id from Keyword k where k.processed = false")
	List<Long> findAllUnprocessed();

	@Transactional
	@Modifying
	@Query("update Keyword k set k.processed = true where k.id = ?1")
	void setToProcessed(long id);

	@Transactional
	@Modifying
	default void deleteByIdWithTransaction(long id) {
		deleteById(id);
	}
}
