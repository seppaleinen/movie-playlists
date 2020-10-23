package se.david.moviesimporter.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Movie;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
}
