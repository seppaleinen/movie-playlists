package se.david.moviesimporter.repository;

import java.util.List;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Keyword;

@Repository
public interface KeywordRepository extends JpaRepository<Keyword, Long> {
	@Transactional
	default List<Keyword> saveAllWithTransaction(List<Keyword> keywords) {
		return saveAll(keywords);
	}
}
