package se.david.moviesimporter.repository;

import java.util.List;
import java.util.stream.Stream;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.Person;

@Repository
public interface PersonRepository extends JpaRepository<Person, Long> {
	@Transactional
	default List<Person> saveAllWithTransaction(List<Person> persons){
		return saveAll(persons);
	}

	@Transactional
	@Query(value = "select p.id from Person p where p.processed = false")
	List<Long> findAllUnprocessed();

	@Transactional
	@Modifying
	@Query("update Person p set p.processed = true where p.id = ?1")
	void setToProcessed(long id);

	@Transactional
	@Modifying
	default void deleteByIdWithTransaction(long id) {
		deleteById(id);
	}
}
