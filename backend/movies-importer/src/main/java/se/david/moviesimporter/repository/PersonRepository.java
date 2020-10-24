package se.david.moviesimporter.repository;

import java.util.List;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Movie;
import se.david.moviesimporter.domain.Person;

@Repository
public interface PersonRepository extends JpaRepository<Person, Long> {
	@Transactional
	default List<Person> saveAllWithTransaction(List<Person> persons){
		return saveAll(persons);
	}
}
