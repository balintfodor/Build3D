#include "Graph.h"

#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <list>

#include "Node.h"

using namespace core::directed_acyclic_graph;
using namespace std;

GraphPtr Graph::create(const std::string& name)
{
    return GraphPtr(new Graph(name));
}

Graph::Graph(const std::string& name) : m_name(name)
{}

bool Graph::empty() const
{
    return m_nodes.empty();
}

size_t Graph::size() const
{
    return m_nodes.size();
}

NodePtr Graph::add(const std::string& name)
{
    m_nodes.push_back(Node::create(name));
    m_nodes.back()->m_owner = shared_from_this();
    return m_nodes.back();
}

NodePtr Graph::add(NodePtr& node)
{
    auto it = find(m_nodes.begin(), m_nodes.end(), node);
    if (it != m_nodes.end()) {
        return node;
    }

    vector<TraversalMode> modes = {TraversalMode::InputsOnly, TraversalMode::OutputsOnly};
    for (auto mode : modes) {
        Traversal t = node->traverse(mode);
        while (t.hasNext()) {
            NodePtr current = t.next();
            if (find(m_nodes.begin(), m_nodes.end(), current) == m_nodes.end()) {
                m_nodes.push_back(current);
            }
            if (current->hasOwner() && current->m_owner.lock() != shared_from_this()) {
                current->m_owner.lock()->remove(current);
            }
            current->m_owner = shared_from_this();
        }
    }

    return node;
}

void Graph::remove(NodePtr& node)
{
    auto it = find(m_nodes.begin(), m_nodes.end(), node);
    if (it != m_nodes.end()) {
        for (auto w : (*it)->m_inputs) {
            w.lock()->disconnect(node);
        }

        for (auto n : (*it)->m_outputs) {
            n->disconnect(node);
        }

        (*it)->m_owner.reset();
        m_nodes.erase(it);
    }
}

void Graph::clear()
{
    for_each(m_nodes.begin(), m_nodes.end(),
        [](NodePtr& n) { n->m_owner.reset(); });
    m_nodes.clear();
}

std::string Graph::name() const
{
    return m_name;
}

Graph::~Graph()
{
    clear();
}