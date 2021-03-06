package directed_graph;

import graph.AbstractEdge;

/**
 * Edge class.
 *
 * @author Ziang Lu
 */
class DirectedEdge extends AbstractEdge {

    /**
     * Tail of this edge.
     */
    private Vertex tail;
    /**
     * Head of this edge.
     */
    private Vertex head;

    /**
     * Constructor with parameter.
     * @param tail tail of this edge
     * @param head head of this edge
     * @param length length of this edge
     */
    DirectedEdge(Vertex tail, Vertex head, double length) {
        super(length);
        this.tail = tail;
        this.head = head;
    }

    /**
     * Accessor of tail.
     * @return tail
     */
    Vertex tail() {
        return tail;
    }

    /**
     * Accessor of head.
     * @return head
     */
    Vertex head() {
        return head;
    }

    /**
     * Mutator of tail.
     * @param tail tail
     */
    void setTail(Vertex tail) {
        this.tail = tail;
    }

    /**
     * Mutator of head.
     * @param head head
     */
    void setHead(Vertex head) {
        this.head = head;
    }

    @Override
    public String toString() {
        return String.format("Edge from Vertex #%d to Vertex #%d with length %lf", tail.id(), head.id(), length);
    }

}
