package br.com.barberagenda.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.barberagenda.model.Barbeiro;
import jakarta.persistence.LockModeType;

public interface BarbeiroRepository extends JpaRepository<Barbeiro, Long> {

    List<Barbeiro> findByAtivoTrueOrderByNomeAsc();

    List<Barbeiro> findAllByOrderByNomeAsc();

    /**
     * Busca o barbeiro com bloqueio de escrita, serializando agendamentos simultâneos
     * para o mesmo barbeiro (evita dois agendamentos sobrepostos criados ao mesmo tempo).
     */
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select b from Barbeiro b where b.id = :id")
    Optional<Barbeiro> buscarComBloqueio(@Param("id") Long id);
}
