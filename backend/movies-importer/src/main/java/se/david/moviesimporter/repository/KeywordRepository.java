package se.david.moviesimporter.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Keyword;

@Repository
public interface KeywordRepository extends JpaRepository<Keyword, Long> {
}
